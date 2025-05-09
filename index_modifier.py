import os
import re

def merge_and_update_html():
    index_html_path = "/home/ubuntu/etlaq_site/index.html"
    industry_info_html_path = "/home/ubuntu/etlaq_site/industry-info.html"
    output_html_path = "/home/ubuntu/etlaq_site/index_merged.html"

    try:
        with open(index_html_path, "r", encoding="utf-8") as f:
            index_content = f.read()

        with open(industry_info_html_path, "r", encoding="utf-8") as f:
            industry_content_full = f.read()

        # Extract content from <main class="container industry-content"> to </main>
        match = re.search(r'<main class="container industry-content">(.*?)<\/main>', industry_content_full, re.DOTALL)
        if not match:
            print("Error: Could not find main content in industry-info.html")
            return
        
        industry_main_content = match.group(1).strip()
        # Remove the initial H1 and the final back button from the extracted content
        industry_main_content = re.sub(r'^<h1>.*?<\/h1>', '', industry_main_content, count=1, flags=re.IGNORECASE | re.DOTALL).strip()
        industry_main_content = re.sub(r'<a href="index.html" class="back-button">.*?<\/a>', '', industry_main_content, flags=re.IGNORECASE | re.DOTALL).strip()

        new_section_id = "industry-info"
        new_section_title = "معلومات عن الصناعة"
        new_section_html = f'''<section id="{new_section_id}">
<h2>{new_section_title}</h2>
{industry_main_content}
</section>'''

        # Insert the new section before the </main> tag in index.html
        main_closing_tag_index = index_content.rfind("</main>")
        if main_closing_tag_index == -1:
            print("Error: Could not find closing </main> tag in index.html")
            return
        
        modified_index_content = index_content[:main_closing_tag_index] + new_section_html + "\n" + index_content[main_closing_tag_index:]

        # Update navigation: remove old link, add new tab link
        old_nav_link_pattern = r'<a href="industry-info.html">معلومات عن الصناعة<\/a>'
        new_nav_link = f'<a href="#{new_section_id}" onclick="showTab(\'{new_section_id}\', this)">{new_section_title}</a>'
        modified_index_content = re.sub(old_nav_link_pattern, new_nav_link, modified_index_content)

        # Update the link in the home section paragraph to point to the new tab
        home_section_link_pattern = r'<a href="industry-info.html">اضغط هنا لمعرفة المزيد عن تقنيات حقن التربة أو الحقن الأسمنتي وكشف التكهفات<\/a>'
        # Ensure onclick JS is properly escaped for HTML attribute
        new_home_section_link_js_onclick = f"document.querySelector('nav a[href=\\'#{new_section_id}\\']').click(); return false;"
        new_home_section_link = f'<a href="#{new_section_id}" onclick="{new_home_section_link_js_onclick}">اضغط هنا لمعرفة المزيد عن تقنيات حقن التربة أو الحقن الأسمنتي وكشف التكهفات</a>'
        modified_index_content = re.sub(home_section_link_pattern, new_home_section_link, modified_index_content)
        
        # Update service areas in "من نحن" (About Us) section
        service_area_text = "<p><strong>مناطق الخدمة:</strong> نخدم جميع أنحاء المملكة: الرياض، جدة، الدمام، المدينة المنورة، القصيم وغيرها.</p>"
        about_section_end_marker = "<!-- Add staff information if desired -->"
        about_section_end_index = modified_index_content.find(about_section_end_marker)
        if about_section_end_index != -1:
            # Insert before the comment marker
            modified_index_content = modified_index_content[:about_section_end_index] + service_area_text + "\n" + modified_index_content[about_section_end_index:]
        else:
            # Fallback: try to insert before the </section> of #about
            about_section_match = re.search(r'(<section id="about">.*?)(<\/section>)', modified_index_content, re.DOTALL | re.IGNORECASE)
            if about_section_match:
                modified_index_content = about_section_match.group(1) + service_area_text + "\n" + about_section_match.group(2) + modified_index_content[about_section_match.end():]
            else:
                print("Warning: Could not find a suitable place in 'من نحن' section to add service areas.")

        # Correct the gallery section which is outside </body> in the original index.html
        gallery_section_match = re.search(r'(<\/body>\s*<\/html>\s*<section id="gallery">.*?<\/section>)', modified_index_content, re.DOTALL | re.IGNORECASE)
        if gallery_section_match:
            gallery_html = gallery_section_match.group(0).replace("</body>", "").replace("</html>", "").strip()
            # Remove it from the end
            modified_index_content = modified_index_content.replace(gallery_section_match.group(0), "</body>\n</html>")
            # Insert gallery before the contact section (or as the last section in main)
            contact_section_start_match = re.search(r'<section id="contact">', modified_index_content, re.IGNORECASE)
            if contact_section_start_match:
                insertion_point = contact_section_start_match.start()
                modified_index_content = modified_index_content[:insertion_point] + gallery_html + "\n" + modified_index_content[insertion_point:]
            else: # Fallback: insert before </main>
                main_closing_tag_index_recheck = modified_index_content.rfind("</main>")
                modified_index_content = modified_index_content[:main_closing_tag_index_recheck] + gallery_html + "\n" + modified_index_content[main_closing_tag_index_recheck:]
            print("Moved gallery section to be within the main content flow.")


        with open(output_html_path, "w", encoding="utf-8") as f:
            f.write(modified_index_content)
        
        print(f"Successfully merged content and updated service areas. New file saved as {output_html_path}")
        
        os.replace(output_html_path, index_html_path)
        print(f"Replaced {index_html_path} with the updated version.")

        if os.path.exists(industry_info_html_path):
            os.remove(industry_info_html_path)
            print(f"Deleted {industry_info_html_path}")
        else:
            print(f"Warning: {industry_info_html_path} not found for deletion.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    merge_and_update_html()
