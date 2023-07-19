using RockPaperScissorsBoom.Core.Game.Results;
using RockPaperScissorsBoom.Core.Model;

namespace RockPaperScissorsBoom.Core.Game.Bots
{
    public class ScissorsOnlyBot : BaseBot
    {
        public ScissorsOnlyBot(Competitor competitor) : base(competitor)
        {
        }
        public override Decision GetDecision(PreviousDecisionResult previousResult) => Decision.Scissors;
    }
}