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
    - **chatgpt_diagram_analysis_notebook.ipynb** _for classifiying images using gpt4o api_
    - **data_classifcation_ocr.ipynb** _for reclassifying data displays and data collection type diagrams from data structure classified or process diagram and conceptual diagram figures_
    - **data_cleaning.ipynb** _basic data exploration notebook_
    - **extract_figure_pages_from_papers.ipynb** _for extracting figure pages from papers via OCR_
    - **sort_papers_by_year.ipynb** _for initial sorting of papers by year into papers_by_year directory_
    - **view_figure_classificaitons_as_html.ipynb** _for making html outputs showing figure classifications_
    - **view_diagram_data_as_html.ipynb** _for making html outputs showing tracked diagram data_
    - **figure_clustering_notebook.ipynb** _for making determining most representative images by subtype/year via clustering analysis_
 
- **papers**

  _folder containing all original papers_

- **papers_by_year**

  _folder containing papers sorted into year directories_

- **streamlit_cropping_labeling_app**

  _folder containing streamlit app, in **image_selection_and_labeling_app.py**, as well as datafile used by streamlit app, **fig_pages_viewed.xlsx**, which is used for tracking which figure pages have been viewed.

- **clustered_images**

  _folder containing images sorted via their clustering analysis, by year. In each yearly folder, you will find🥇

    - **conceptual diagram** _the output for clustering analysis on conceptual diagram subcategory_
    - **process diagram** _the output for clustering analysis on process diagram subcategory_
    - **process_and_conceptual** _the output for clustering analysis on subcategory of either process diagram or conceptual diagram_
    - **diagram_type** _the output for clustering analysis on subcategory of any diagram type_
    - **no_photos_drawings_other** _the output for clustering analysis on subcategory of any type except photo, drawing, or other_
  
    **Note: figures that represent the figure closest to the center of clusters will be in most_representatie folder within subcategory clusters. for example, for the most representive conceptual diagram image from 2020 will be in       figure_averaging/clustered_images/2020/conceptual diagram/most_representative/** 
