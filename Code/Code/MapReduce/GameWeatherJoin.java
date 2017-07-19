import java.io.IOException;
import java.net.URI;
import java.net.URISyntaxException;
import java.util.LinkedList;
import java.util.List;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.input.FileSplit;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

public class GameWeatherJoin {
  public static final String DELIMITER = ",";

  static class GameWeatherMappper
      extends Mapper<LongWritable, Text, Text, Text> {
    @Override
    protected void map(LongWritable key, Text value,
        Mapper<LongWritable, Text, Text, Text>.Context context)
        throws IOException, InterruptedException {

      FileSplit split = (FileSplit) context.getInputSplit();
      String filePath = split.getPath().toString();
      String line = value.toString();
      if (line == null || line.trim().equals(""))
        return;

      String[] values = line.split(DELIMITER);

      if (filePath.contains("weather.csv")) {
        try {
          context.write(new Text(values[0]),
              new Text("w#" + values[2] + DELIMITER
                  + values[8] + DELIMITER + values[14] + DELIMITER + values[17]
                  + DELIMITER + values[21]));
        } catch (IndexOutOfBoundsException e) {
          System.out.println(values[0]);
        }
      }

      else if (filePath.contains("game.csv")) {
        try {
          context.write(new Text(values[0]),
              new Text("g#" + values[1] + DELIMITER + values[2] + DELIMITER
                  + values[3] + DELIMITER + values[4] + DELIMITER + values[5]
                  + DELIMITER + values[6] + DELIMITER + values[7] + DELIMITER
                  + values[8] + DELIMITER + values[9] + DELIMITER + values[10]
                  + DELIMITER + values[11]));
        } catch (IndexOutOfBoundsException e) {
          System.out.println(values[0]);
        }
      }
    }
  }

  static class GameWeatherReducer extends Reducer<Text, Text, Text, Text> {
    @Override
    protected void reduce(Text key, Iterable<Text> values,
        Reducer<Text, Text, Text, Text>.Context context)
        throws IOException, InterruptedException {

      List<String> linkU = new LinkedList<String>();
      List<String> linkL = new LinkedList<String>();

      for (Text tval : values) {
        String val = tval.toString();
        if (val.startsWith("w#")) {
          linkU.add(val.substring(2));
        } else if (val.startsWith("g#")) {
          linkL.add(val.substring(2));
        }
      }

      for (String u : linkU) {
        for (String l : linkL) {
          context.write(key, new Text(u + DELIMITER + l));
        }
      }
    }
  }

  public static void main(String[] args) throws IOException,
      ClassNotFoundException, InterruptedException, URISyntaxException {

    Job job = new Job();
    job.setJarByClass(GameWeatherJoin.class);
    job.setJobName("Game Weather Data Join");

    FileInputFormat.addInputPath(job, new Path(args[0]));
    FileOutputFormat.setOutputPath(job, new Path(args[1]));

    job.setMapperClass(GameWeatherMappper.class);
    job.setReducerClass(GameWeatherReducer.class);

    job.setOutputKeyClass(Text.class);
    job.setOutputValueClass(Text.class);

    System.exit(job.waitForCompletion(true) ? 0 : 1);
  }

}
