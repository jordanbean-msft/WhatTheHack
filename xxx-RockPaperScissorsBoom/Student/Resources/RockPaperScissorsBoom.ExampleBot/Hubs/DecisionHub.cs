using Microsoft.AspNetCore.SignalR;
using RockPaperScissorsBoom.Core.Game.Bots;
using RockPaperScissorsBoom.Core.Game.Results;
using RockPaperScissorsBoom.Core.Model;

namespace RockPaperScissorsBoom.ExampleBot.Hubs
{
    public class DecisionHub : Hub
    {
        public async Task RequestMove(PreviousDecisionResult previousDecisionResult)
        {
            var cleverBot = new CleverBot(new Competitor("ExampleBot", "ExampleBot"));
            var decision = cleverBot.GetDecision(previousDecisionResult);
            await Clients.Caller.SendAsync("ReceiveMove", decision);
        }
    }
}
