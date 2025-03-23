using MongoDB.Bson.Serialization.Attributes;
using MongoDB.Bson;
using System.ComponentModel.DataAnnotations;

public class FertilizerInput
{
    [BsonId]
    [BsonRepresentation(BsonType.ObjectId)]
    public string Id { get; set; }

    [Required]
    public DateTime ProvidedDateTime { get; set; }

    [Required]
    public bool IsActive { get; set; }

    [Required]
    public string RaspberrypiId { get; set; }
}
