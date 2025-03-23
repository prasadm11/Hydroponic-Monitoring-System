using MongoDB.Bson;
using MongoDB.Bson.Serialization.Attributes;

public class PhInfo
{
    [BsonId]
    [BsonRepresentation(BsonType.ObjectId)]
    public string Id { get; set; }

    public double PHValue { get; set; }
    public DateTime CreatedDate { get; set; }
    public string RaspberrypiId { get; set; }
}
