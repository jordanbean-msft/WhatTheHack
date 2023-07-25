using RockPaperScissorsBoom.Core.Game;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace RockPaperScissorsBoom.Core.SignalRBot
{
    public interface ISignalRBotClient
    {
        Task MakeDecisionAsync(Decision decision);
    }
}
