using FoundryChat.Models;
using FoundryChat.Services;
using Microsoft.Extensions.FileProviders;

var builder = WebApplication.CreateBuilder(args);

// Add services to the container
builder.Services.AddControllers();
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

// Configure Foundry settings
var foundrySettings = new FoundrySettings();
builder.Configuration.GetSection("Foundry").Bind(foundrySettings);

// Register HttpClient for FoundryClient
builder.Services.AddHttpClient<IFoundryClient, FoundryClient>()
    .ConfigureHttpClient(client =>
    {
        client.Timeout = TimeSpan.FromSeconds(foundrySettings.ResponseTimeout);
    });

// Register FoundrySettings as singleton
builder.Services.AddSingleton(foundrySettings);

// Add CORS
builder.Services.AddCors(options =>
{
    options.AddDefaultPolicy(policy =>
    {
        policy.AllowAnyOrigin()
              .AllowAnyMethod()
              .AllowAnyHeader();
    });
});

var app = builder.Build();

// Configure the HTTP request pipeline
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseHttpsRedirection();

// Enable CORS
app.UseCors();

// Serve static files from wwwroot
var wwwrootPath = Path.Combine(builder.Environment.ContentRootPath, "wwwroot");
if (Directory.Exists(wwwrootPath))
{
    app.UseDefaultFiles();
    app.UseStaticFiles();
}

app.UseRouting();
app.UseAuthorization();

// Map controllers
app.MapControllers();

// Map fallback to index.html for SPA routing
if (Directory.Exists(wwwrootPath))
{
    app.MapFallbackToFile("index.html");
}

// Log configuration on startup
var logger = app.Services.GetRequiredService<ILogger<Program>>();
logger.LogInformation("Foundry Chat Application Starting");
logger.LogInformation($"Foundry Enabled: {foundrySettings.Enabled}");
if (foundrySettings.Enabled)
{
    logger.LogInformation($"Foundry Endpoint: {foundrySettings.Endpoint}");
    logger.LogInformation($"Foundry Project: {foundrySettings.Project}");
    logger.LogInformation($"Foundry Application: {foundrySettings.Application}");
    logger.LogInformation($"Use Azure Identity: {foundrySettings.UseAzureIdentity}");
}

app.Run();

