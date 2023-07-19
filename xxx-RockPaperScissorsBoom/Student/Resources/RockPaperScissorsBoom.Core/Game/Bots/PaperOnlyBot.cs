using RockPaperScissorsBoom.Core.Game.Results;
using RockPaperScissorsBoom.Core.Model;

namespace RockPaperScissorsBoom.Core.Game.Bots
{
    public class PaperOnlyBot : BaseBot
    {
        public PaperOnlyBot(Competitor competitor) : base(competitor)
        {
        }
        public override Decision GetDecision(PreviousDecisionResult previousResult) => Decision.Paper;
    }
}