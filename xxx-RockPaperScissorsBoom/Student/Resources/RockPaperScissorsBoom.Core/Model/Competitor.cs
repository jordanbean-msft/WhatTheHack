using System;

namespace RockPaperScissorsBoom.Core.Model
{
    public class Competitor : BaseEntity
    {
        public string Name { get; set; }
        public string BotType { get; set; }
        public string? Url { get; set; }

        public Competitor(string name, string botType)
        {
            Name = name;
            BotType = botType;
        }
    }
}