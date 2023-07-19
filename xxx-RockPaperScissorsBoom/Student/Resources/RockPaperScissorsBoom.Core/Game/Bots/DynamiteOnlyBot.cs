using RockPaperScissorsBoom.Core.Game.Results;
using RockPaperScissorsBoom.Core.Model;

namespace RockPaperScissorsBoom.Core.Game.Bots
{
    public class DynamiteOnlyBot : BaseBot
    {
        public DynamiteOnlyBot(Competitor competitor) : base(competitor)
        {
        }
        public override Decision GetDecision(PreviousDecisionResult previousResult) => Decision.Dynamite;
    }
}