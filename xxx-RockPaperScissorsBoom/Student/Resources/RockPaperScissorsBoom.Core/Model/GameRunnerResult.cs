using System.Collections.Generic;

namespace RockPaperScissorsBoom.Core.Model
{
    public class GameRunnerResult
    {
        public GameRecord? GameRecord { get; set; }
        public List<FullResults>? AllMatchResults { get; set; }
    }
}