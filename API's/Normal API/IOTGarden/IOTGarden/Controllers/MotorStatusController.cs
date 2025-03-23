// Controllers/MotorStatusController.cs
//using IOTGarden.Controllers;
using Microsoft.AspNetCore.Mvc;
using MongoDB.Driver;
using System.Collections.Generic;
using System.Threading.Tasks;

[Route("api/[controller]")]
[ApiController]
public class MotorStatusController : ControllerBase
{
    private readonly IoTContext _context;

    public MotorStatusController(IoTContext context)
    {
        _context = context;
    }

    [HttpGet]
    public async Task<ActionResult<IEnumerable<MotorStatus>>> GetMotorStatuses()
    {
        var motorStatuses = await _context.MotorStatuses.Find(_ => true).ToListAsync();
        return Ok(motorStatuses);
    }

    [HttpGet("{id}")]
    public async Task<ActionResult<MotorStatus>> GetMotorStatus(string id)
    {
        var motorStatus = await _context.MotorStatuses.Find(p => p.Id == id).FirstOrDefaultAsync();
        if (motorStatus == null)
        {
            return NotFound();
        }
        return Ok(motorStatus);
    }




    [HttpPost]
    public async Task<ActionResult<MotorStatus>> PostMotorStatus(MotorStatus motorStatus)
    {
        await _context.MotorStatuses.InsertOneAsync(motorStatus);
        return CreatedAtAction(nameof(GetMotorStatus), new { id = motorStatus.Id }, motorStatus);
    }

    [HttpPut("{id}")]
    public async Task<IActionResult> PutMotorStatus(string id, MotorStatus motorStatus)
    {
        var filter = Builders<MotorStatus>.Filter.Eq(p => p.Id, id);
        var updateResult = await _context.MotorStatuses.ReplaceOneAsync(filter, motorStatus);
        if (updateResult.IsAcknowledged && updateResult.ModifiedCount > 0)
        {
            return NoContent();
        }
        return NotFound();
    }

    [HttpDelete("{id}")]
    public async Task<IActionResult> DeleteMotorStatus(string id)
    {
        var deleteResult = await _context.MotorStatuses.DeleteOneAsync(p => p.Id == id);
        if (deleteResult.IsAcknowledged && deleteResult.DeletedCount > 0)
        {
            return NoContent();
        }
        return NotFound();
    }
}
