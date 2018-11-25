package imdbImageMiner;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.MalformedURLException;
import java.net.URL;

import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.nodes.Node;
import org.jsoup.select.Elements;

public class Miner {

	// Reads an html page and returns its text as string
	public static String ReadPage(String name) {
		URL url;
		InputStream is = null;
		BufferedReader br;
		String line;

		StringBuilder strBuilder = new StringBuilder();

		try {
			url = new URL(name);
			is = url.openStream(); // throws an IOException
			br = new BufferedReader(new InputStreamReader(is));

			while ((line = br.readLine()) != null) {
				// System.out.println(line);
				strBuilder.append(line);
			}
		} catch (MalformedURLException mue) {
			mue.printStackTrace();
		} catch (IOException ioe) {
			ioe.printStackTrace();
		} finally {
			try {
				if (is != null)
					is.close();
			} catch (IOException ioe) {
				// nothing to see here
			}
		}

		return strBuilder.toString();
	}

	public static void main(String[] args) throws IOException {
		// TODO Auto-generated method stub

		// A useful imdb with a lot of movies
		// https://www.imdb.com/list/ls057823854/?sort=list_order,asc&st_dt=&mode=detail&page=2
		String baseUrl = "https://www.imdb.com/list/ls057823854/?sort=list_order,asc&st_dt=&mode=detail&page=";

		PrintWriter writer = new PrintWriter("imdb-urls2.txt", "UTF-8");
		
		for (int page = 100; page < 101; page++) {

			String url = baseUrl + page;
			String html = ReadPage(url);	
			Document doc = Jsoup.parse(html);

			System.out.println("Downloaded html of page " + page + " ("+url+")");

			// Find all images
			//Elements imgs = doc.getElementsByClass("lister-item-image ribbonize");
			Elements imgs = doc.select("img");
			
			for (Element img : imgs) {
				if(img.hasAttr("data-tconst"))
					writer.println( img.attr("data-tconst") + "\t" + img.attr("alt") + "\t" + img.attr("loadlate") );
			}
			
			/*
			for (Element img : imgs) {
				
				Node child =  img.childNode(0);
				System.out.println(img.childNode(0).attr("href"));
				
				System.out.println("Child nodes: " + child.childNodeSize());
				
				//if( img.hasAttr("data-tconst") )
				System.out.println( child.childNode(1).attr("data-tconst") + "\t" + child.childNode(1).attr("alt") + "\t" + child.childNode(1).attr("src") );
				
			}
*/
		}
		
		writer.close();
	}

}
