using System;
using System.IO;
using System.Threading.Tasks;
using System.Threading;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Azure.WebJobs;
using Microsoft.Azure.WebJobs.Extensions.Http;
using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.Logging;
using Newtonsoft.Json;

namespace Daniel.Bench
{
    public static class BenchFunc
    {
        [FunctionName("BenchFunc")]
        public static async Task<IActionResult> Run(
            [HttpTrigger(AuthorizationLevel.Anonymous, "get", "post", Route = null)] HttpRequest req,
            Microsoft.Azure.WebJobs.ExecutionContext functionContext,
            ILogger log)
        {
            var init = DateTimeOffset.Now.ToUnixTimeMilliseconds();
            log.LogInformation("C# HTTP trigger function START.");

            var id = functionContext.InvocationId;
            string instanceId = Environment.GetEnvironmentVariable("WEBSITE_INSTANCE_ID");

            DoWork();
            // DoSleep();

            log.LogInformation("C# HTTP trigger function END.");
            var end = DateTimeOffset.Now.ToUnixTimeMilliseconds();

            var res = new
            {
                Init = init,
                End = end,
                InvocationID = id,
                InstanceID = instanceId
            };
            // string responseMessage = $"{init}, {end}, {id}";
            string responseMessage = JsonConvert.SerializeObject(res);
            return new OkObjectResult(responseMessage);
        }

        private static void DoSleep()
        {
            Thread.Sleep(1000);
        }

        private static void DoWork()
        {
            // MonteCarlo sim PI
            int iterations = 20_000_000;
            var rand = new System.Random();

            int count = 0;
            double x, y;
            for (int i = 0; i < iterations; i++)
            {
                x = rand.NextDouble();
                y = rand.NextDouble();
                if (x * x + y * y <= 1.0)
                {
                    count++;
                }
            }
            double pi = 4.0 * count / iterations;
            // Console.WriteLine(pi);
        }
    }
}
