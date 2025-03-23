using MongoDB.Bson;
using MongoDB.Bson.Serialization.Attributes;
using System.ComponentModel.DataAnnotations;

public class PhInfo
{
    [BsonId]
    [BsonRepresentation(BsonType.ObjectId)]
    public string Id { get; set; }

    [Required]
    public double PHValue { get; set; }

    [Required]
    public DateTime CreatedDate { get; set; }

    [Required]
    public string RaspberrypiId { get; set; }
}