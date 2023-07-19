using Microsoft.AspNetCore.SignalR.Client;
using RockPaperScissorsBoom.Core.Game;
using RockPaperScissorsBoom.Core.Game.Bots;
using RockPaperScissorsBoom.Core.Game.Results;
using RockPaperScissorsBoom.Core.Model;

namespace RockPaperScissorsBoom.Server.Bot
{
    public class SignalRBot : BaseBot
    {
        private HubConnection? _connection;
        private Decision? _decision = null;

        public string ApiRootUrl { get; set; }

        public SignalRBot(Competitor competitor): base(competitor)
        {
            ApiRootUrl = competitor.Url ?? "";
        }

        private void InitializeConnection()
        {
            if (_connection != null) 
                return;

            _connection = new HubConnectionBuilder()
                .WithUrl(ApiRootUrl)
                .Build();
            _connection.StartAsync().Wait();

            _connection.On<Decision>("MakeDecision", (decision) =>
            {
                _decision = decision;
            });

        }

        public override Decision GetDecision(PreviousDecisionResult previousResult)
        {
            if (_connection == null) InitializeConnection();

            _connection?.InvokeAsync("RequestMove", previousResult);

            while (_decision == null)
            {
            }

            var decisionToReturn = _decision;
            _decision = null;
            return decisionToReturn.Value;
        }
    }
}