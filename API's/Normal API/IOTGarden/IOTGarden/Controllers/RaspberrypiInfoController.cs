// Controllers/RaspberrypiInfoController.cs
//using IOTGarden.Controllers;
using Microsoft.AspNetCore.Mvc;
using MongoDB.Driver;
using System.Collections.Generic;
using System.Threading.Tasks;

[Route("api/[controller]")]
[ApiController]
public class RaspberrypiInfoController : ControllerBase
{
    private readonly IoTContext _context;

    public RaspberrypiInfoController(IoTContext context)
    {
        _context = context;
    }

    [HttpGet]
    public async Task<ActionResult<IEnumerable<RaspberrypiInfo>>> GetRaspberrypiInfos()
    {
        var raspberrypiInfos = await _context.RaspberrypiInfos.Find(_ => true).ToListAsync();
        return Ok(raspberrypiInfos);
    }

    [HttpGet("{id}")]
    public async Task<ActionResult<RaspberrypiInfo>> GetRaspberrypiInfo(string id)
    {
        var raspberrypiInfo = await _context.RaspberrypiInfos.Find(p => p.Id == id).FirstOrDefaultAsync();
        if (raspberrypiInfo == null)
        {
            return NotFound();
        }
        return Ok(raspberrypiInfo);
    }



    [HttpPost]
    public async Task<ActionResult<RaspberrypiInfo>> PostRaspberrypiInfo(RaspberrypiInfo raspberrypiInfo)
    {
        await _context.RaspberrypiInfos.InsertOneAsync(raspberrypiInfo);
        return CreatedAtAction(nameof(GetRaspberrypiInfo), new { id = raspberrypiInfo.Id }, raspberrypiInfo);
    }

    [HttpPut("{id}")]
    public async Task<IActionResult> PutRaspberrypiInfo(string id, RaspberrypiInfo raspberrypiInfo)
    {
        var filter = Builders<RaspberrypiInfo>.Filter.Eq(p => p.Id, id);
        var updateResult = await _context.RaspberrypiInfos.ReplaceOneAsync(filter, raspberrypiInfo);
        if (updateResult.IsAcknowledged && updateResult.ModifiedCount > 0)
        {
            return NoContent();
        }
        return NotFound();
    }

    [HttpDelete("{id}")]
    public async Task<IActionResult> DeleteRaspberrypiInfo(string id)
    {
        var deleteResult = await _context.RaspberrypiInfos.DeleteOneAsync(p => p.Id == id);
        if (deleteResult.IsAcknowledged && deleteResult.DeletedCount > 0)
        {
            return NoContent();
        }
        return NotFound();
    }
}
