import { useState } from 'react'
import axios from 'axios'
import Api from './Api/ApiConfig';

import './App.css'

function App() {
  
  const [inputText, setInputText] = useState('');
  const [selectedImage, setSelectedImage] = useState(null);
  const [responseData, setResponseData] = useState(null);
  const [error, setError] = useState(null);

  const handleImageChange = (event) => {
    setSelectedImage(event.target.files[0]);
  };
  const handleSubmit = async (event) => {
    event.preventDefault();

    const formData = new FormData();
    formData.append('text', inputText);

    if (selectedImage) {
      formData.append('image', selectedImage,selectedImage.name);
    }

    try {
      const response = await axios.post('http://127.0.0.1:8000/detect/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      if (response.status !== 200) {
        throw new Error(`API request failed with status ${response.status}`);
      }
      console.log(response.data)
      setResponseData(response.data);
      console.log(responseData)
      setError(null);
    } catch (error) {
      console.error('Error sending data to API:', error);
      setError(error.message);
    }
  };


  
    // function handleChange(e) {
    //     console.log(e.target.files);
    //     setFile(URL.createObjectURL(e.target.files[0]));
    // }

   
  
      // const handleSubmit = async () => {
      //   if (!file) {
      //     return alert('Please select an image');
      //   }
    
      //   const formData = new FormData();
      //   formData.append('file', file);

      //   console.log(formData);
    
      //   Api.post("detect/", formData[0], {
      //     headers: {
      //       "Content-Type": "multipart/form-data",
     
      //     }
      //   }).then((res) => {
      //     console.log(res.data);
          
      //   });
      // }
 
    
        return (
          <div>
    <form onSubmit={handleSubmit}>
      <label htmlFor="inputText">Enter Text:</label>
      <input
        id="inputText"
        type="text"
        value={inputText}
        
        onChange={(e) => setInputText(e.target.value)}
      />
       <label htmlFor="imageFile">Select Image (optional):</label>
      <input
        id="imageFile"
        type="file"
        accept="image/*"
        onChange={handleImageChange}
      />
      <button type="submit">Send Text</button>
    </form>
   
    </div>
  );
}

   


export default App;
