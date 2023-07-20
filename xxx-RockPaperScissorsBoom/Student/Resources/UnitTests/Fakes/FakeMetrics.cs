using System.Collections.Generic;
using RockPaperScissorsBoom.Core.Game;
using RockPaperScissorsBoom.Core.Game.Bots;
using RockPaperScissorsBoom.Core.Game.Results;
using RockPaperScissorsBoom.Core.Model;

namespace UnitTests.Fakes
{
    public class FakeMetrics : IMetrics
    {
        public void TrackEventDuration(string eventName, Dictionary<string, string?> properties, Dictionary<string, double> metrics)
        {
            return;
        }
    }
}