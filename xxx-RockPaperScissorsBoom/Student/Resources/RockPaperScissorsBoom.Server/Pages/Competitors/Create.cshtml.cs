using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.AspNetCore.Mvc.Rendering;
using RockPaperScissorsBoom.Core.Model;
using RockPaperScissorsBoom.Server.Data;

namespace RockPaperScissorsBoom.Server.Pages.Competitors
{
    public class CreateModel : PageModel
    {
        private readonly RockPaperScissorsBoom.Server.Data.ApplicationDbContext _context;

        public CreateModel(RockPaperScissorsBoom.Server.Data.ApplicationDbContext context)
        {
            _context = context;
        }

        public IActionResult OnGet()
        {
            return Page();
        }

        [BindProperty]
        public Competitor Competitor { get; set; } = default!;
        

        // To protect from overposting attacks, see https://aka.ms/RazorPagesCRUD
        public async Task<IActionResult> OnPostAsync()
        {
          if (!ModelState.IsValid || _context.Competitors == null || Competitor == null)
            {
                return Page();
            }

            _context.Competitors.Add(Competitor);
            await _context.SaveChangesAsync();

            return RedirectToPage("./Index");
        }
    }
}
