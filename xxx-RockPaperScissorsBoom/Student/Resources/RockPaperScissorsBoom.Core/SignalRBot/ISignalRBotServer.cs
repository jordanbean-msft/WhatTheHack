using RockPaperScissorsBoom.Core.Game.Results;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace RockPaperScissorsBoom.Core.SignalRBot
{
    public interface ISignalRBotServer
    {
        public Task RequestMoveAsync(PreviousDecisionResult previousDecisionResult);
    }
}
