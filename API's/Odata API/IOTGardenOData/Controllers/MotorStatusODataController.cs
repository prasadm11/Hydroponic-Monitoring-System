using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.OData.Query;
using Microsoft.AspNetCore.OData.Routing.Controllers;
using IOTGarden.Models;
using IOTGarden.OData;
using MongoDB.Bson;
using Microsoft.AspNetCore.OData.Formatter;
using Microsoft.AspNetCore.OData.Results;
using MongoDB.Driver;

namespace IOTGardenOData.Controllers
{
    [Route("odata/MotorStatusOData")]
    public class MotorStatusODataController : ODataController
    {
        private readonly IoTContext _context;

        public MotorStatusODataController(IoTContext context)
        {
            _context = context;
        }

        // GET: odata/MotorStatusOData
        [HttpGet]
        [EnableQuery]
        public IQueryable<MotorStatus> Get()
        {
            return _context.MotorStatuses.AsQueryable();
        }

        // GET: odata/MotorStatusOData(5)
        [HttpGet("({key})")]
        [EnableQuery]
        public SingleResult<MotorStatus> Get([FromODataUri] string key)
        {
            return SingleResult.Create(_context.MotorStatuses.AsQueryable().Where(m => m.Id == key));
        }

        // POST: odata/MotorStatusOData
        [HttpPost]
        public IActionResult Post([FromBody] MotorStatus motorStatus)
        {
            if (!ModelState.IsValid)
            {
                return BadRequest(ModelState);
            }

            _context.MotorStatuses.InsertOne(motorStatus);
            return Created(motorStatus);
        }
    }
}
