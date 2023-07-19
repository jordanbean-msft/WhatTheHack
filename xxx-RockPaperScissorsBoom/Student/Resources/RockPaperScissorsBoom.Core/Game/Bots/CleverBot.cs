using RockPaperScissorsBoom.Core.Game.Results;
using RockPaperScissorsBoom.Core.Model;

namespace RockPaperScissorsBoom.Core.Game.Bots
{
    public class CleverBot : BaseBot
    {
        public CleverBot(Competitor competitor) : base(competitor)
        {
        }

        public override Decision GetDecision(PreviousDecisionResult? previousResult)
        {
            return GetDecisionThatBeats(previousResult?.OpponentPrevious);
        }

        public static Decision GetDecisionThatBeats(Decision? decisionToBeat)
        {
            return decisionToBeat switch
            {
                Decision.Rock => Decision.Paper,
                Decision.Paper => Decision.Scissors,
                Decision.Scissors => Decision.Rock,
                Decision.WaterBalloon => Decision.Rock,
                Decision.Dynamite => Decision.WaterBalloon,
                _ => Decision.Rock,
            };
        }
    }
}