﻿using FluentAssertions;
using Microsoft.Extensions.Logging.Abstractions;
using RockPaperScissorsBoom.Core.Game;
using RockPaperScissorsBoom.Core.Game.Bots;
using RockPaperScissorsBoom.Core.Game.Results;
using RockPaperScissorsBoom.Core.Model;
using UnitTests.DataBuilders;
using UnitTests.Fakes;

namespace UnitTests.Core.Game.RoundRunnerTests
{
    public class RunRoundShould
    {
        private readonly RockOnlyBot _rockOnlyBot
            = new(new Competitor("", ""), new NullLogger<RunRoundShould>());
        private readonly PaperOnlyBot _paperOnlyBot
            = new(new Competitor("", ""), new NullLogger<RunRoundShould>());
        private readonly WaterOnlyBot _waterOnlyBot
            = new(new Competitor("", ""), new NullLogger<RunRoundShould>());
        private readonly DynamiteOnlyBot _dynamiteOnlyBot
            = new(new Competitor("", ""), new NullLogger<RunRoundShould>());
        private readonly ScissorsOnlyBot _scissorsOnlyBot
            = new(new Competitor("", ""), new NullLogger<RunRoundShould>());
        private readonly RoundRunner _roundRunner = new();
        private readonly RoundResultBuilder _builder = new();

        [Fact]
        public async void ReturnResultsOfRound_GivenSimpleWinCase()
        {
            RoundResult roundResult = await _roundRunner.RunRound(_rockOnlyBot, _scissorsOnlyBot, _builder.WithDefaults().Build(), new FakeMetrics(), 0);

            roundResult.Winner.Should().Be(_rockOnlyBot.Competitor);
            roundResult.Player1.Should().Be(_rockOnlyBot.Competitor);
            roundResult.Player2.Should().Be(_scissorsOnlyBot.Competitor);
            roundResult.Player1Played.Should().Be(Decision.Rock);
            roundResult.Player2Played.Should().Be(Decision.Scissors);
        }

        [Fact]
        public async void ReturnNoWinner_GivenSameChoice()
        {
            RoundResult roundResult = await _roundRunner.RunRound(_rockOnlyBot, _rockOnlyBot, _builder.WithDefaults().Build(), new FakeMetrics(), 0);

            roundResult.Winner.Should().BeNull();
        }

        [Fact]
        public async void ReturnCorrectWinner_GivenSimpleWins()
        {
            RoundResult rockWin = await _roundRunner.RunRound(_rockOnlyBot, _scissorsOnlyBot, _builder.WithDefaults().Build(), new FakeMetrics(), 0);
            rockWin.Winner.Should().Be(_rockOnlyBot.Competitor);

            RoundResult paperWin = await _roundRunner.RunRound(_paperOnlyBot, _rockOnlyBot, _builder.WithDefaults().Build(), new FakeMetrics(), 0);
            paperWin.Winner.Should().Be(_paperOnlyBot.Competitor);

            RoundResult scissorsWin = await _roundRunner.RunRound(_scissorsOnlyBot, _paperOnlyBot, _builder.WithDefaults().Build(), new FakeMetrics(), 0);
            scissorsWin.Winner.Should().Be(_scissorsOnlyBot.Competitor);

            RoundResult dynamiteWin = await _roundRunner.RunRound(_dynamiteOnlyBot, _rockOnlyBot, _builder.WithDefaults().Build(), new FakeMetrics(), 0);
            dynamiteWin.Winner.Should().Be(_dynamiteOnlyBot.Competitor);

            RoundResult waterWin = await _roundRunner.RunRound(_waterOnlyBot, _dynamiteOnlyBot, _builder.WithDefaults().Build(), new FakeMetrics(), 0);
            waterWin.Winner.Should().Be(_waterOnlyBot.Competitor);
        }

        [Fact]
        public async void IncrementDyanmite_GivenOneDynamiteUsage()
        {
            int previousUsage = _dynamiteOnlyBot.DynamiteUsed;
            await _roundRunner.RunRound(_dynamiteOnlyBot, _rockOnlyBot, _builder.WithDefaults().Build(), new FakeMetrics(), 0);
            _dynamiteOnlyBot.DynamiteUsed.Should().Be(previousUsage + 1);
        }

        [Fact]
        public async void IncrementDyanmite_GivenTwoDynamiteUsage()
        {
            int previousUsage = _dynamiteOnlyBot.DynamiteUsed;
            await _roundRunner.RunRound(_dynamiteOnlyBot, _dynamiteOnlyBot, _builder.WithDefaults().Build(), new FakeMetrics(), 0);
            _dynamiteOnlyBot.DynamiteUsed.Should().Be(previousUsage + 2);
        }

        [Fact]
        public async void IncrementDyanmite_EvenWhenInvalid()
        {
            int previousUsage = _dynamiteOnlyBot.DynamiteUsed;
            var fakeBot = new FakeBot(Decision.Dynamite, new NullLogger<RunRoundShould>(), 10)
            {
                Competitor = new Competitor("test", "")
            };
            await _roundRunner.RunRound(_dynamiteOnlyBot, fakeBot, _builder.WithDefaults().Build(), new FakeMetrics(), 0);
            _dynamiteOnlyBot.DynamiteUsed.Should().Be(previousUsage + 1);
            fakeBot.DynamiteUsed.Should().Be(11);
        }
    }
}