using MongoDB.Bson;
using MongoDB.Bson.Serialization.Attributes;

public class WaterLevel
{
    [BsonId]
    [BsonRepresentation(BsonType.ObjectId)]
    public string Id { get; set; } // BSON ID

    public string TankId { get; set; }
    public DateTime WaterPushedOn { get; set; }
    public double Percentage { get; set; }
    public string RaspberrypiId { get; set; }
}
