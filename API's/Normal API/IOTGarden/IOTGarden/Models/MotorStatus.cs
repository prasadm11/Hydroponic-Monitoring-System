using MongoDB.Bson;
using MongoDB.Bson.Serialization.Attributes;
using System.ComponentModel.DataAnnotations;

public class MotorStatus
{
    [BsonId]
    [BsonRepresentation(BsonType.ObjectId)]
    public string Id { get; set; }

    [Required]
    public DateTime StartTimeDate { get; set; }

    [Required]
    public DateTime EndTimeDate { get; set; }

    [Required]
    public string RaspberrypiId { get; set; }

    [Required]
    public bool IsActive { get; set; }
}