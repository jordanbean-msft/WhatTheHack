using RockPaperScissorsBoom.Core.Game.Results;
using RockPaperScissorsBoom.Core.Model;

namespace RockPaperScissorsBoom.Core.Game.Bots
{
    public class WaterOnlyBot : BaseBot
    {
        public WaterOnlyBot(Competitor competitor) : base(competitor)
        {
        }
        public override Decision GetDecision(PreviousDecisionResult previousResult) => Decision.WaterBalloon;
    }
}