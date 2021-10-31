using System;
using System.IO;
using Microsoft.Azure.WebJobs;
using Microsoft.Azure.WebJobs.Host;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Configuration;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using System.Data;
using System.Linq;


namespace AzureFunction
{
    [StorageAccount("BlobConnectionString")]
    public static class AzureFunction
    {
        [FunctionName("AzureFunction")]
        public static void Run([BlobTrigger("ytw-iot-test/{name}")]Stream inputBlob, 
            //[Blob("azure-func-output/{name}", FileAccess.Write)] Stream outputBlob,
            string name, ILogger log)
        {
            log.LogInformation($"C# Blob trigger function Processed blob\n Name:{name} \n Size: {inputBlob.Length} Bytes");

           

            try
            {
                log.LogInformation("Received a new file");
                if (name.EndsWith(".json"))
                {
                    log.LogInformation("Received a new json file");
                    StreamReader reader = new StreamReader(inputBlob);
                    string jsonContent = reader.ReadToEnd();
                    //dynamic json = JObject.Parse(jsonContent);
                    log.LogInformation(jsonContent);
                    
                }
                
            }
            catch (Exception e)
            {

                log.LogError("Receive fails", e);
            }
        }
    }
}
