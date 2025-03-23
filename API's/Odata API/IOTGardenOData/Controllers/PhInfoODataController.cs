using IOTGarden.OData;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.OData.Formatter;
using Microsoft.AspNetCore.OData.Query;
using Microsoft.AspNetCore.OData.Results;
using Microsoft.AspNetCore.OData.Routing.Controllers;
using MongoDB.Driver;

namespace IOTGardenOData.Controllers
{
    [Route("odata/PhInfoOData")]
    public class PhInfoODataController : ODataController
    {
        private readonly IoTContext _context;

        public PhInfoODataController(IoTContext context)
        {
            _context = context;
        }

        // GET: odata/PhInfoOData
        [HttpGet]
        [EnableQuery]
        public IQueryable<PhInfo> Get()
        {
            return _context.PhInfos.AsQueryable();
        }

        // GET: odata/PhInfoOData(5)
        [HttpGet("({key})")]
        [EnableQuery]
        public SingleResult<PhInfo> Get([FromODataUri] string key)
        {
            return SingleResult.Create(_context.PhInfos.AsQueryable().Where(f => f.Id == key));
        }

        // POST: odata/PhInfoOData
        [HttpPost]
        public IActionResult Post([FromBody] PhInfo phInfo)
        {
            if (!ModelState.IsValid)
            {
                return BadRequest(ModelState);
            }

            _context.PhInfos.InsertOne(phInfo);
            return Created(phInfo);
        }
    }
}
