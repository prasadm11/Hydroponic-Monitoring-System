using IOTGarden.OData;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.OData.Formatter;
using Microsoft.AspNetCore.OData.Query;
using Microsoft.AspNetCore.OData.Results;
using Microsoft.AspNetCore.OData.Routing.Controllers;
using MongoDB.Driver;

namespace IOTGardenOData.Controllers
{
    [Route("odata/RaspberrypiInfoOData")]
    public class RaspberrypiInfoODataController : ODataController
    {
        private readonly IoTContext _context;

        public RaspberrypiInfoODataController(IoTContext context)
        {
            _context = context;
        }

        // GET: odata/RaspberrypiInfoOData
        [HttpGet]
        [EnableQuery]
        public IQueryable<RaspberrypiInfo> Get()
        {
            return _context.RaspberrypiInfos.AsQueryable();
        }

        // GET: odata/RaspberrypiInfoOData(5)
        [HttpGet("({key})")]
        [EnableQuery]
        public SingleResult<RaspberrypiInfo> Get([FromODataUri] string key)
        {
            return SingleResult.Create(_context.RaspberrypiInfos.AsQueryable().Where(f => f.Id == key));
        }

        // POST: odata/RaspberrypiInfoOData
        [HttpPost]
        public IActionResult Post([FromBody] RaspberrypiInfo raspberrypiInfo)
        {
            if (!ModelState.IsValid)
            {
                return BadRequest(ModelState);
            }

            _context.RaspberrypiInfos.InsertOne(raspberrypiInfo);
            return Created(raspberrypiInfo);
        }
    }
}
