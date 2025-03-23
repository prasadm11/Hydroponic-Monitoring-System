using MongoDB.Bson;
using MongoDB.Bson.Serialization.Attributes;

public class MotorStatus
{
    [BsonId]
    [BsonRepresentation(BsonType.ObjectId)]

    public string Id { get; set; }

    public DateTime StartTimeDate { get; set; }
    public DateTime EndTimeDate { get; set; }
    public string RaspberrypiId { get; set; }
    public bool IsActive { get; set; }
}
