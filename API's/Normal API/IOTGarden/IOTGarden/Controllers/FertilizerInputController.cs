// Controllers/FertilizerInputController.cs
//using IOTGarden.Controllers;
using Microsoft.AspNetCore.Mvc;
using MongoDB.Driver;
using System.Collections.Generic;
using System.Threading.Tasks;

[Route("api/[controller]")]
[ApiController]
public class FertilizerInputController : ControllerBase
{
    private readonly IoTContext _context;

    public FertilizerInputController(IoTContext context)
    {
        _context = context;
    }

    [HttpGet]
    public async Task<ActionResult<IEnumerable<FertilizerInput>>> GetFertilizerInputs()
    {
        var fertilizerInputs = await _context.FertilizerInputs.Find(_ => true).ToListAsync();
        return Ok(fertilizerInputs);
    }

    [HttpGet("{id}")]
    public async Task<ActionResult<FertilizerInput>> GetFertilizerInput(string id)
    {
        var fertilizerInput = await _context.FertilizerInputs.Find(p => p.Id == id).FirstOrDefaultAsync();
        if (fertilizerInput == null)
        {
            return NotFound();
        }
        return Ok(fertilizerInput);
    }


    [HttpPost]
    public async Task<ActionResult<FertilizerInput>> PostFertilizerInput(FertilizerInput fertilizerInput)
    {
        await _context.FertilizerInputs.InsertOneAsync(fertilizerInput);
        return CreatedAtAction(nameof(GetFertilizerInput), new { id = fertilizerInput.Id }, fertilizerInput);
    }

    [HttpPut("{id}")]
    public async Task<IActionResult> PutFertilizerInput(string id, FertilizerInput fertilizerInput)
    {
        var filter = Builders<FertilizerInput>.Filter.Eq(p => p.Id, id);
        var updateResult = await _context.FertilizerInputs.ReplaceOneAsync(filter, fertilizerInput);
        if (updateResult.IsAcknowledged && updateResult.ModifiedCount > 0)
        {
            return NoContent();
        }
        return NotFound();
    }


    [HttpDelete("{id}")]
    public async Task<IActionResult> DeleteFertilizerInput(string id)
    {
        var deleteResult = await _context.FertilizerInputs.DeleteOneAsync(p => p.Id == id);
        if (deleteResult.IsAcknowledged && deleteResult.DeletedCount > 0)
        {
            return NoContent();
        }
        return NotFound();
    }
}
