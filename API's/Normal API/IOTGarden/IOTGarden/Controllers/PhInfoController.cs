//using IOTGarden.Controllers;
using Microsoft.AspNetCore.Mvc;
using MongoDB.Driver;
using System.Threading.Tasks;

[Route("api/[controller]")]
[ApiController]
public class PhInfoController : ControllerBase
{
    private readonly IoTContext _context;

    public PhInfoController(IoTContext context)
    {
        _context = context;
    }

    [HttpGet]
    public async Task<ActionResult<IEnumerable<PhInfo>>> GetPhInfos()
    {
        var phInfos = await _context.PhInfos.Find(_ => true).ToListAsync();
        return Ok(phInfos);
    }

    [HttpGet("{id}")]
    public async Task<ActionResult<PhInfo>> GetPhInfo(string id)
    {
        var phInfo = await _context.PhInfos.Find(p => p.Id == id).FirstOrDefaultAsync();
        if (phInfo == null)
        {
            return NotFound();
        }
        return Ok(phInfo);
    }




    [HttpPost]
    public async Task<ActionResult<PhInfo>> PostPhInfo(PhInfo phInfo)
    {
        await _context.PhInfos.InsertOneAsync(phInfo);
        return CreatedAtAction(nameof(GetPhInfo), new { id = phInfo.Id }, phInfo);
    }

    [HttpPut("{id}")]
    public async Task<IActionResult> PutPhInfo(string id, PhInfo phInfo)
    {
        var filter = Builders<PhInfo>.Filter.Eq(p => p.Id, id);
        var updateResult = await _context.PhInfos.ReplaceOneAsync(filter, phInfo);
        if (updateResult.IsAcknowledged && updateResult.ModifiedCount > 0)
        {
            return NoContent();
        }
        return NotFound();
    }

    [HttpDelete("{id}")]
    public async Task<IActionResult> DeletePhInfo(string id)
    {
        var deleteResult = await _context.PhInfos.DeleteOneAsync(p => p.Id == id);
        if (deleteResult.IsAcknowledged && deleteResult.DeletedCount > 0)
        {
            return NoContent();
        }
        return NotFound();
    }
}