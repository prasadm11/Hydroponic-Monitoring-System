using MongoDB.Bson;
using MongoDB.Bson.Serialization.Attributes;
using System.ComponentModel.DataAnnotations;

public class RaspberrypiInfo
{
    [BsonId]
    [BsonRepresentation(BsonType.ObjectId)]
    public string Id { get; set; }

    [Required]
    public string RaspberrypiName { get; set; }

    [Required]
    public DateTime CreatedDate { get; set; }

    [Required]
    public bool IsActive { get; set; }
}