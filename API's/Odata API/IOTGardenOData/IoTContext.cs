using IOTGarden.Models;
using MongoDB.Driver;

namespace IOTGarden.OData
{
    public class IoTContext
    {
        private readonly IMongoDatabase _database;

        public IoTContext()
        {
            const string connectionUri = "mongodb+srv://prasadmahajan6735:Prasad%405050@mongodbcrud.ugxblmb.mongodb.net/?retryWrites=true&w=majority\r\n";
            var settings = MongoClientSettings.FromConnectionString(connectionUri);
            settings.ServerApi = new ServerApi(ServerApiVersion.V1);

            var client = new MongoClient(settings);
            _database = client.GetDatabase("MongoDBCRUD"); // Ensure the database name matches
        }

        public IMongoCollection<FertilizerInput> FertilizerInputs => _database.GetCollection<FertilizerInput>("FertilizerInput");
        public IMongoCollection<MotorStatus> MotorStatuses => _database.GetCollection<MotorStatus>("MotorStatus");

        public IMongoCollection<PhInfo> PhInfos => _database.GetCollection<PhInfo>("PhInfo");

        public IMongoCollection<RaspberrypiInfo> RaspberrypiInfos => _database.GetCollection<RaspberrypiInfo>("RaspberrypiInfo");

        public IMongoCollection<WaterLevel> WaterLevels => _database.GetCollection<WaterLevel>("WaterLevel");
    }
}
