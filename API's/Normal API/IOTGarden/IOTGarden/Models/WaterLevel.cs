using MongoDB.Bson;
using MongoDB.Bson.Serialization.Attributes;
using System.ComponentModel.DataAnnotations;

public class WaterLevel
{
    [BsonId]
    [BsonRepresentation(BsonType.ObjectId)]
    public string Id { get; set; }

    [Required]
    public string TankId { get; set; }

    [Required]
    public DateTime WaterPushedOn { get; set; }

    [Required]
    public double Percentage { get; set; }

    [Required]
    public string RaspberrypiId { get; set; }
}