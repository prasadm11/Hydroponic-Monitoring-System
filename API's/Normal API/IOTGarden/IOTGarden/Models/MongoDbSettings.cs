// File: Models/MongoDbSettings.cs

namespace IOTGarden.Models // Replace 'MyApi' with your actual project namespace
{
    public class MongoDbSettings
    {
        public string ConnectionString { get; set; }
        public string DatabaseName { get; set; }
        public string Username { get; set; }
        public string Password { get; set; }
    }
}
