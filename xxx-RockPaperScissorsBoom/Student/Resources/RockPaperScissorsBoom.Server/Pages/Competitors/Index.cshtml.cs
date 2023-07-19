using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.EntityFrameworkCore;
using RockPaperScissorsBoom.Core.Model;
using RockPaperScissorsBoom.Server.Data;

namespace RockPaperScissorsBoom.Server.Pages.Competitors
{
    public class IndexModel : PageModel
    {
        private readonly RockPaperScissorsBoom.Server.Data.ApplicationDbContext _context;

        public IndexModel(RockPaperScissorsBoom.Server.Data.ApplicationDbContext context)
        {
            _context = context;
        }

        public IList<Competitor> Competitor { get;set; } = default!;

        public async Task OnGetAsync()
        {
            if (_context.Competitors != null)
            {
                Competitor = await _context.Competitors.ToListAsync();
            }
        }
    }
}
