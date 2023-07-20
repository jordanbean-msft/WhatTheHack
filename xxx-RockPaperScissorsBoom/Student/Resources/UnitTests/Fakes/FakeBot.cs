using RockPaperScissorsBoom.Core.Game;
using RockPaperScissorsBoom.Core.Game.Bots;
using RockPaperScissorsBoom.Core.Game.Results;
using RockPaperScissorsBoom.Core.Model;

namespace UnitTests.Fakes
{
    public class FakeBot : BaseBot
    {
        private readonly Decision _decision;

        public FakeBot(Decision decision, int dynamiteUsed = 0) : base(new Competitor("", ""))
        {
            _decision = decision;
            DynamiteUsed = dynamiteUsed;
        }

        public override Decision GetDecision(PreviousDecisionResult previousResult)
        {
            return _decision;
        }
    }
}