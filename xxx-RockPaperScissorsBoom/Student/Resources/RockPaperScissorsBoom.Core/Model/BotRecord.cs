namespace RockPaperScissorsBoom.Core.Model
{
    public class BotRecord : BaseEntity
    {
        public GameRecord? GameRecord { get; set; }
        public Competitor? Competitor { get; set; }
        public int Wins { get; set; }
        public int Losses { get; set; }
        public int Ties { get; set; }

        public BotRecord()
        {

        }

        public BotRecord(GameRecord gameRecord, Competitor competitor, int wins, int losses, int ties)
        {
            GameRecord = gameRecord;
            Competitor = competitor;
            Wins = wins;
            Losses = losses;
            Ties = ties;
        }
    }
}