using IOTGarden.OData;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.OData.Formatter;
using Microsoft.AspNetCore.OData.Query;
using Microsoft.AspNetCore.OData.Results;
using Microsoft.AspNetCore.OData.Routing.Controllers;
using MongoDB.Driver;

namespace IOTGardenOData.Controllers
{
    [Route("odata/WaterLevelOData")]
    public class WaterLevelODataController : ODataController
    {
        private readonly IoTContext _context;

        public WaterLevelODataController(IoTContext context)
        {
            _context = context;
        }

        // GET: odata/WaterLevelOData
        [HttpGet]
        [EnableQuery]
        public IQueryable<WaterLevel> Get()
        {
            return _context.WaterLevels.AsQueryable();
        }

        // GET: odata/WaterLevelOData(5)
        [HttpGet("({key})")]
        [EnableQuery]
        public SingleResult<WaterLevel> Get([FromODataUri] string key)
        {
            return SingleResult.Create(_context.WaterLevels.AsQueryable().Where(w => w.Id == key));
        }

        // POST: odata/WaterLevelOData
        [HttpPost]
        public IActionResult Post([FromBody] WaterLevel waterLevel)
        {
            if (!ModelState.IsValid)
            {
                return BadRequest(ModelState);
            }

            _context.WaterLevels.InsertOne(waterLevel);
            return Created(waterLevel);
        }
    }
}
