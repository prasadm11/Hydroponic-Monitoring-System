//using IOTGarden.Controllers;
using Microsoft.AspNetCore.Mvc;
using MongoDB.Driver;
using System.Collections.Generic;
using System.Threading.Tasks;

[Route("api/[controller]")]
[ApiController]
public class WaterLevelController : ControllerBase
{
    private readonly IoTContext _context;

    public WaterLevelController(IoTContext context)
    {
        _context = context;
    }

    [HttpGet]
    public async Task<ActionResult<IEnumerable<WaterLevel>>> GetWaterLevels()
    {
        var waterLevels = await _context.WaterLevels.Find(_ => true).ToListAsync();
        return Ok(waterLevels);
    }

    [HttpGet("{id}")]
    public async Task<ActionResult<WaterLevel>> GetWaterLevel(string id)
    {
        var waterLevel = await _context.WaterLevels.Find(p => p.Id == id).FirstOrDefaultAsync();
        if (waterLevel == null)
        {
            return NotFound();
        }
        return Ok(waterLevel);
    }




    [HttpPost]
    public async Task<ActionResult<WaterLevel>> PostWaterLevel(WaterLevel waterLevel)
    {
        await _context.WaterLevels.InsertOneAsync(waterLevel);
        return CreatedAtAction(nameof(GetWaterLevel), new { id = waterLevel.Id }, waterLevel);
    }

    [HttpPut("{id}")]
    public async Task<IActionResult> PutWaterLevel(string id, WaterLevel waterLevel)
    {
        var filter = Builders<WaterLevel>.Filter.Eq(p => p.Id, id);
        var updateResult = await _context.WaterLevels.ReplaceOneAsync(filter, waterLevel);
        if (updateResult.IsAcknowledged && updateResult.ModifiedCount > 0)
        {
            return NoContent();
        }
        return NotFound();
    }

    [HttpDelete("{id}")]
    public async Task<IActionResult> DeleteWaterLevel(string id)
    {
        var deleteResult = await _context.WaterLevels.DeleteOneAsync(p => p.Id == id);
        if (deleteResult.IsAcknowledged && deleteResult.DeletedCount > 0)
        {
            return NoContent();
        }
        return NotFound();
    }
}