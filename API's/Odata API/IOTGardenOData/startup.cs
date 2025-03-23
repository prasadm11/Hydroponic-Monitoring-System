using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Hosting;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using Microsoft.OData.ModelBuilder;
using Microsoft.AspNetCore.OData;
using Microsoft.OpenApi.Models;
using IOTGarden.Models;
using IOTGarden.OData;
using IOTGardenOData.Controllers;
using Microsoft.AspNetCore.OData.Formatter;
using Microsoft.Net.Http.Headers;
using System.Net;
using MongoDB.Driver;
using Microsoft.Extensions.DependencyInjection;
public class Startup
{
    public void ConfigureServices(IServiceCollection services)
    {
        services.AddControllers(mvcOptions =>
        {
            mvcOptions.EnableEndpointRouting = false;
        }).AddOData(opt =>
        {
            var builder = new ODataConventionModelBuilder();
            builder.EntitySet<FertilizerInput>("FertilizerInputOData");
            builder.EntitySet<MotorStatus>("MotorStatusOData");
            builder.EntitySet<PhInfo>("PhInfoOData");
            builder.EntitySet<RaspberrypiInfo>("RaspberrypiInfoOData");
            builder.EntitySet<WaterLevel>("WaterLevelOData");
            opt.AddRouteComponents("odata", builder.GetEdmModel());
            opt.Select().Expand().Filter().OrderBy().Count().SetMaxTop(null).EnableQueryFeatures();
        });

        services.AddControllers().AddJsonOptions(options =>
        {
            options.JsonSerializerOptions.PropertyNamingPolicy = null;
            options.JsonSerializerOptions.DictionaryKeyPolicy = null;
        });


        // Register IoTContext with dependency injection
        services.AddSingleton<IoTContext>(sp =>
        {
            var connectionString = "mongodb+srv://prasadmahajan6735:Prasad%405050@mongodbcrud.ugxblmb.mongodb.net/?retryWrites=true&w=majority\r\n"; // Replace with your actual connection string
            var databaseName = "MongoDBCRUD"; // Replace with your actual database name
            return new IoTContext();
        });
        services.AddSwaggerGen(c =>
        {
            c.SwaggerDoc("v1", new OpenApiInfo { Title = "IoTGarden API", Version = "v1" });
            
        });
        AddFormatters(services);
    }

    public void Configure(IApplicationBuilder app, IWebHostEnvironment env)
    {
        if (env.IsDevelopment())
        {
            app.UseDeveloperExceptionPage();
        }

        app.UseRouting();
        app.UseAuthorization();
        app.UseEndpoints(endpoints =>
        {
            endpoints.MapControllers();
        });
        app.UseSwagger();
        app.UseSwaggerUI(c => c.SwaggerEndpoint("/swagger/v1/swagger.json", "IoTGarden API v1"));
    }

    private static Microsoft.OData.Edm.IEdmModel GetEdmModel()
    {
        var builder = new ODataConventionModelBuilder();

        // Define your entity sets here
        builder.EntitySet<FertilizerInput>("FertilizerInputOData");
        builder.EntitySet<PhInfo>("PhInfoOData");
        builder.EntitySet<WaterLevel>("WaterLevelOData");
        builder.EntitySet<MotorStatus>("MotorStatusOData");
        builder.EntitySet<RaspberrypiInfo>("RaspberrypiInfoOData");

        return builder.GetEdmModel();
    }

    private void AddFormatters(IServiceCollection services)
    {
        services.AddMvcCore(options =>
        {
            foreach (var outputFormatter in options.OutputFormatters.OfType<ODataOutputFormatter>().Where(_ => _.SupportedMediaTypes.Count == 0))
            {
                outputFormatter.SupportedMediaTypes.Add(new MediaTypeHeaderValue("application/prs.odatatestxx-odata"));
            }
            foreach (var inputFormatter in options.InputFormatters.OfType<ODataInputFormatter>().Where(_ => _.SupportedMediaTypes.Count == 0))
            {
                inputFormatter.SupportedMediaTypes.Add(new MediaTypeHeaderValue("application/prs.odatatestxx-odata"));
            }
        });
    }
}

