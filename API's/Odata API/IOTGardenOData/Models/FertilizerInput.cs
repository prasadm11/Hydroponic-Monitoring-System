using MongoDB.Bson;
using MongoDB.Bson.Serialization.Attributes;
using System;

namespace IOTGarden.Models
{
    public class FertilizerInput
    {
        [BsonId]
        [BsonRepresentation(BsonType.ObjectId)]
        public string Id { get; set; }

        public DateTime ProvidedDateTime { get; set; }

        public bool IsActive { get; set; }

        public string RaspberrypiId { get; set; }
    }
}
