using System.Linq;
using FluentAssertions;
using RockPaperScissorsBoom.Core.Game;
using RockPaperScissorsBoom.Core.Game.Bots;
using RockPaperScissorsBoom.Core.Model;
using UnitTests.Fakes;
using Xunit;

namespace UnitTests.Core.Game.GameRunnerTests
{
    public class StartAllMatchesShould
    {
        [Fact]
        public void ReturnEmpty_GivenNoBots()
        {
            var gameRunner = new GameRunner(new FakeMetrics());

            var result = gameRunner.StartAllMatches();

            result.GameRecord.BotRecords.Should().BeEmpty();
        }

        [Fact]
        public void ReturnOneBot_GivenOneBotCompeting()
        {
            var gameRunner = new GameRunner(new FakeMetrics());
            gameRunner.AddBot(new RockOnlyBot(new Competitor("", "")));

            var result = gameRunner.StartAllMatches();

            result.GameRecord.BotRecords.Should().ContainSingle();
        }
    }
}