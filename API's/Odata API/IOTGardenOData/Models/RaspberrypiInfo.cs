using MongoDB.Bson;
using MongoDB.Bson.Serialization.Attributes;

public class RaspberrypiInfo
{
    [BsonId]
    [BsonRepresentation(BsonType.ObjectId)]
    public string Id { get; set; } // BSON ID

    public string RaspberrypiName { get; set; }
    public DateTime CreatedDate { get; set; }
    public bool IsActive { get; set; }
}
