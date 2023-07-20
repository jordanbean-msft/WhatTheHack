using Microsoft.AspNetCore.Mvc.RazorPages;
using RockPaperScissorsBoom.Core.Game.Bots;
using RockPaperScissorsBoom.Core.Game;
using RockPaperScissorsBoom.Core.Model;
using RockPaperScissorsBoom.Server.Bot;
using RockPaperScissorsBoom.Server.Data;
using RockPaperScissorsBoom.Server.Helpers;
using RockPaperScissorsBoom.Server.Models;
using Microsoft.EntityFrameworkCore;

namespace RockPaperScissorsBoom.Server.Pages
{
    public class RunTheGameModel : PageModel
    {
        private readonly ApplicationDbContext db;
        private readonly IMetrics metrics;
        private readonly IConfiguration configuration;
        private readonly IMessagingHelper messageHelper;

        public List<BotRecord> BotRankings { get; set; } = new List<BotRecord>();
        public List<FullResults> AllFullResults { get; set; } = new List<FullResults>();

        public List<GameRecord> GamesForTable { get; set; } = new List<GameRecord>();

        public RunTheGameModel(ApplicationDbContext db, IMetrics metrics, IConfiguration configuration, IMessagingHelper messageHelper)
        {
            this.db = db;
            this.metrics = metrics;
            this.configuration = configuration;
            this.messageHelper = messageHelper;
        }

        public void OnGet()
        {
            GameRecord gameRecord = db.GameRecords
                .Include(x => x.BotRecords)
                .ThenInclude(x => x.Competitor)
                .OrderByDescending(x => x.GameDate)
                .FirstOrDefault();

            AllFullResults = new List<FullResults>();

            GamesForTable = db.GameRecords.OrderByDescending(g => g.GameDate).Take(10).Include(g => g.BotRecords).ToList();
        }

        public async Task OnPostAsync()
        {
            List<Competitor> competitors = db.Competitors.ToList();
            if (!competitors.Any())
            {
                competitors = GetDefaultCompetitors();
                db.Competitors.AddRange(competitors);
                db.SaveChanges();
            }

            var gameRunner = new GameRunner(metrics);
            foreach (var competitor in competitors)
            {
                BaseBot bot = CreateBotFromCompetitor(competitor);
                gameRunner.AddBot(bot);
            }

            var stopwatch = System.Diagnostics.Stopwatch.StartNew();

            GameRunnerResult gameRunnerResult = gameRunner.StartAllMatches();

            stopwatch.Stop();

            var metric = new Dictionary<string, double> { { "GameLength", stopwatch.Elapsed.TotalMilliseconds } };

            // Set up some properties:
            var properties = new Dictionary<string, string?> { { "Source", configuration["P20HackFestTeamName"] } };

            // Send the event:
            metrics.TrackEventDuration("GameRun", properties, metric);

            SaveResults(gameRunnerResult);
            BotRankings = gameRunnerResult.GameRecord.BotRecords.OrderByDescending(x => x.Wins).ToList();
            AllFullResults = gameRunnerResult.AllMatchResults.OrderBy(x => x.Competitor.Name).ToList();

            //Get 10 Last 
            GamesForTable = db.GameRecords.OrderByDescending(g => g.GameDate).Take(10).Include(g => g.BotRecords).ToList();

            if (bool.Parse(configuration["EventGridOn"] ?? "false"))
            {
                await PublishMessage(BotRankings.First().GameRecord?.Id.ToString() ?? "", BotRankings.First().Competitor?.Name ?? "");
            }
        }

        internal async Task PublishMessage(string GameId, string Winner)
        {
            var msg = new GameMessage
            {
                GameId = GameId,
                Winner = Winner,
                Hostname = HttpContext.Request.Host.Host,
                TeamName = configuration["P20HackFestTeamName"]
            };
            await messageHelper.PublishMessageAsync("RockPaperScissors.GameWinner.RunTheGamePage", "Note", DateTime.UtcNow, msg);
        }

        private void SaveResults(GameRunnerResult gameRunnerResult)
        {
            if (gameRunnerResult.GameRecord.BotRecords.Any())
            {
                db.GameRecords.Add(gameRunnerResult.GameRecord);
                db.SaveChanges();
            }
        }

        private static BaseBot CreateBotFromCompetitor(Competitor competitor)
        {
            Type type = Type.GetType(competitor.BotType) ?? throw new Exception($"Could not find type {competitor.BotType}");
            var bot = Activator.CreateInstance(type, competitor) as BaseBot ?? throw new Exception($"Could not create instance of type {competitor.BotType}");
            
            if (bot is SignalRBot signalRBot)
            {
                signalRBot.ApiRootUrl = competitor.Url ?? "";
            }

            return bot;
        }

        private static List<Competitor> GetDefaultCompetitors()
        {
            var competitors = new List<Competitor>
            {
                new Competitor("Rocky", typeof(RockOnlyBot).AssemblyQualifiedName ?? ""),
                new Competitor("Treebeard", typeof(PaperOnlyBot).AssemblyQualifiedName ?? ""),
                new Competitor("Sharpy", typeof(ScissorsOnlyBot).AssemblyQualifiedName ?? ""),
                new Competitor("All Washed Up", typeof(WaterOnlyBot).AssemblyQualifiedName ?? ""),
                new Competitor("Clever Bot", typeof(CleverBot).AssemblyQualifiedName ?? ""),
                new Competitor("Smart Bot", typeof(SmartBot).AssemblyQualifiedName ?? ""),
                //new Competitor
                //{
                //    Name = "Signals",
                //    BotType = typeof(SignalRBot).AssemblyQualifiedName,
                //    Url = "https://localhost:44347/decision"
                //},
                new Competitor("Rando Carrisian", typeof(RandomBot).AssemblyQualifiedName ?? "")
            };
            return competitors;
        }
    }
}
