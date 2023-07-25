using RockPaperScissorsBoom.Core.Game.Bots;
using RockPaperScissorsBoom.Core.Game.Results;
using RockPaperScissorsBoom.Core.Model;
using System.Collections.Concurrent;

namespace RockPaperScissorsBoom.Core.Game
{
    public class MatchRunner
    {
        private readonly IMetrics metrics;
        public int NumberOfRounds { get; } = 100;
        public event EventHandler<MatchCompletedEventArgs>? MatchCompleted;
        public event EventHandler<MatchRoundCompletedEventArgs>? MatchRoundCompleted;

        public MatchRunner(IMetrics metrics)
        {
            this.metrics = metrics;
        }
        public async Task<MatchResult> RunMatch(BaseBot player1, BaseBot player2, int gameNumber, int totalGames)
        {
            var roundResults = new List<RoundResult>(NumberOfRounds);
            var matchResult = new MatchResult(player1.Competitor, player2.Competitor);
            var roundRunner = new RoundRunner();
            roundRunner.RoundCompleted += RoundRunner_RoundCompleted;

            RoundResult previousResult = new(matchResult);
            
            for (int roundNumber = 0; roundNumber < NumberOfRounds; roundNumber++)
            {
                previousResult = await roundRunner.RunRound(player1, player2, previousResult, metrics, roundNumber);                
                roundResults.Add(previousResult);
            }
            
            matchResult = GetMatchResultFromRoundResults(matchResult, player1, roundResults);
            
            OnMatchCompleted(new MatchCompletedEventArgs(matchResult, gameNumber, totalGames));

            return matchResult;
        }

        private void RoundRunner_RoundCompleted(object? sender, RoundCompletedEventArgs e)
        {
            OnMatchRoundCompleted(new MatchRoundCompletedEventArgs(e.RoundResult, e.RoundNumber, NumberOfRounds));
        }

        private static MatchResult GetMatchResultFromRoundResults(MatchResult matchResult,
            BaseBot player1, List<RoundResult> roundResults)
        {
            var winner = roundResults.GroupBy(x => x.Winner).OrderByDescending(x => x.Count()).Select(x => x.Key).First();
            if (winner == null)
            {
                matchResult.WinningPlayer = MatchOutcome.Neither;
            }
            else if (Equals(winner, player1.Competitor))
            {
                matchResult.WinningPlayer = MatchOutcome.Player1;
            }
            else
            {
                matchResult.WinningPlayer = MatchOutcome.Player2;
            }

            matchResult.RoundResults = roundResults;

            return matchResult;
        }

        protected virtual void OnMatchCompleted(MatchCompletedEventArgs e)
        {
            MatchCompleted?.Invoke(this, e);
        }

        protected virtual void OnMatchRoundCompleted(MatchRoundCompletedEventArgs e)
        {
            MatchRoundCompleted?.Invoke(this, e);
        }
    }

    public class MatchCompletedEventArgs : EventArgs
    {
        public MatchResult MatchResult { get; set; }
        public int GameNumber { get; set; }
        public int TotalGames { get; set; }

        public MatchCompletedEventArgs(MatchResult matchResult, int gameNumber, int totalGames)
        {
            MatchResult = matchResult;
            GameNumber = gameNumber;
            TotalGames = totalGames;
        }
    }

    public class MatchRoundCompletedEventArgs : EventArgs
    {
        public RoundResult RoundResult { get; set; }
        public int RoundNumber { get; set; }
        public int TotalRounds { get; set; }

        public MatchRoundCompletedEventArgs(RoundResult roundResult, int roundNumber, int totalRounds)
        {
            RoundResult = roundResult;
            RoundNumber = roundNumber;
            TotalRounds = totalRounds;
        }
    }
}