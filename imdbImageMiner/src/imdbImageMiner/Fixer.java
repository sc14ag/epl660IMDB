package imdbImageMiner;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.HashMap;

import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;

public class Fixer {

	// Loads both urls and csv file
	// Tries to connect them by name
	public static void main(String[] args) throws FileNotFoundException, IOException {
		// TODO Auto-generated method stub

		HashMap<String,String> nameToUrl = new HashMap<String,String>();
		
		// Read url file
		File file = new File("imdb-urls.txt");
		try (BufferedReader br = new BufferedReader(new FileReader(file))) {
		    String line;
		    while ((line = br.readLine()) != null) {
		       // process the line.
		    	String[] tokens = line.split("\t");
		    	
		    	String name = tokens[1].toLowerCase();
		    	// Name as key, Url as value
		    	nameToUrl.put(name, tokens[2]);
		    }
		}
		
		PrintWriter writer = new PrintWriter("IMDB-withImageLinks.csv", "UTF-8");
		
		
		// Read second file
		int notFound = 0;
		int found = 0;
		file = new File("IMDB-Movie-Data.csv");
		try (BufferedReader br = new BufferedReader(new FileReader(file))) {
		    String line;
		    int skipLine = 265;
		    
		    while ((line = br.readLine()) != null) {
		    	
		    	if(skipLine > 0){
		    		// Write line back to file
		    		skipLine--;
		    		writer.println(line);
		    		continue;
		    	}
		    	
		       // process the line.
		    	String[] tokens = line.split(",");
		    	String name = tokens[1].toLowerCase();
		    	
		    	
		    	if( nameToUrl.containsKey(name) ){
		    		String url = nameToUrl.get(name);
		    		System.out.println( tokens[1]+"\t"+url);
		    		
		    		writer.print(line);
		    		writer.println(","+url);
		    		
		    		found++;
		    	}
		    	else{
		    		
		    		
		    		//System.out.println("WARNING: "+tokens[1] + " could not be found in hashmap!");
		    		notFound++;
		    		
		    		String searchTerm = tokens[1].replace(' ', '+');
		    		
		    		// If NOT found, use IMDB search to find it (search by title name!)
		    		String url = "https://www.imdb.com/find?ref_=nv_sr_fn&q="+searchTerm+"&s=tt"; 
					String html = Miner.ReadPage(url);	
					Document doc = Jsoup.parse(html);
		    		
					// Get first of search results
					Elements results = doc.getElementsByClass("result_text");
					Element firstResult = results.first();
					Element child = firstResult.child(0);
					url = "https://www.imdb.com"+child.attr("href");

					// Visit new page with the poster image
					html = Miner.ReadPage(url);	
					doc = Jsoup.parse(html);
					
					Element poster = doc.getElementsByClass("poster").first();
					if( poster != null ){
						Element img = poster.selectFirst("img");
						
			    		System.out.println( tokens[1] + "\t" + img.attr("src"));
			    		
			    		writer.print(line);
			    		writer.println(","+img.attr("src"));
					}
					
		    	}
		    	
		    	
		    }
		    
		    System.out.println("Found: "+found);
		    System.out.println("Not found: "+notFound);
		    
		}
		
		writer.close();
		
		
	}

}
