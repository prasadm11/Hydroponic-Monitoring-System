using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.OData.Query;
using Microsoft.AspNetCore.OData.Routing.Controllers;
using IOTGarden.Models;
using IOTGarden.OData;
using MongoDB.Bson;
using Microsoft.AspNetCore.OData.Formatter;
using Microsoft.AspNetCore.OData.Results;
using MongoDB.Driver;

namespace IOTGarden.Controllers
{

    [Route("odata/[controller]")]
    public class FertilizerInputODataController : ODataController
    {
        private readonly IoTContext _context;

        public FertilizerInputODataController(IoTContext context)
        {
            _context = context;
        }

        // GET: odata/FertilizerInputOData
        [HttpGet("odata/FertilizerInputOData")]
        [EnableQuery]
        public IQueryable<FertilizerInput> Get()
        {
            return _context.FertilizerInputs.AsQueryable();
        }

        // GET: odata/FertilizerInputOData(5)
        [HttpGet("odata/FertilizerInputOData({key})")]
        [EnableQuery]
        public SingleResult<FertilizerInput> Get([FromODataUri] string key)
        {
            return SingleResult.Create(_context.FertilizerInputs.AsQueryable().Where(f => f.Id == key));
        }

        // POST: odata/FertilizerInputOData

        [HttpPost("odata/FertilizerInputOData")]
        public IActionResult Post([FromBody] FertilizerInput fertilizerInput)
        {
            if (!ModelState.IsValid)
            {
                return BadRequest(ModelState);
            }

            _context.FertilizerInputs.InsertOne(fertilizerInput);
            return Created(fertilizerInput);
        }
    }
}
