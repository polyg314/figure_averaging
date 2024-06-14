# figure_averaging

- **cropped_and_labeled_image_data**
  
    _xlsx files contained the cropped image paths, original paper reference paths, and figure classifactions, by year_

- **extracted_figure_pages**
  
    _folder containing all pages extracted from pdfs with Figure keywords detected via OCR. arranged by year_
    _folder also contains **extracted_figure_pages.xlsx**, which is a list of all pages with figures extracted, by paper and figure number detected, as well as **no_extracted_figure_papers.xlsx**, a file with all papers that did not have any figures extracted

- **final_figures**

  _folder with all extracted figures from papers, arranged by year_

- **image_classification_html_outputs**

  _folder with visual html outputs for looking at figure classifications easily_

- **notebooks**

  _folder with all notebooks that are used for various tasks within project, including:__

    - **chatgpt_classification_notebook.ipynb** _for classifiying images using gpt4o api_
    - **extract_figure_pages_from_papers.ipynb** _for extracting figure pages from papers via OCR_
    - **sort_papers_by_year.ipynb** _for initial sorting of papers by year into papers_by_year directory_
    - **view_figure_classificaitons_as_html.ipynb** _for making html outputs showing figure classifications_
 
- **papers**

  _folder containing all original papers_

- **papers_by_year**

  _folder containing papers sorted into year directories_

- **streamlit_cropping_labeling_app**

  _folder containing streamlit app, in **image_selection_and_labeling_app.py**, as well as datafile used by streamlit app, **fig_pages_viewed.xlsx**, which is used for tracking which figure pages have been viewed.

  
  
