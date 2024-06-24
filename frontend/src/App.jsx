import { useState } from 'react'
import axios from 'axios'
import 'bootstrap/dist/css/bootstrap.min.css';



import './App.css'

function App() {
  
  
  const [selectedImage, setSelectedImage] = useState(null);
  const [responseData, setResponseData] = useState(null);
  const [error, setError] = useState(null);

  const handleImageChange = (event) => {
    setSelectedImage(event.target.files[0]);
  };
  const handleSubmit = async (event) => {
    event.preventDefault();

    const formData = new FormData();
    

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


  
  
 
    
        return (
          <div className="container mt-5">
      <form onSubmit={handleSubmit}>
       

        <div className="mb-3">
          <label htmlFor="imageFile" className="form-label">Select Image :</label>
          <input
            id="imageFile"
            type="file"
            className="form-control"
            accept="image/*"
            onChange={handleImageChange}
          />
        </div>

        <button type="submit" className="btn btn-primary">Send Text</button>
      </form>
      
       {responseData && (
        <div className="container mt-5">
          <h2>Data Table</h2>
          <table className="table table-bordered table-striped">
            <thead className="table-dark">
              <tr>
                <th>Parameter</th>
                <th>Value 1</th>
                <th>Value 2</th>
                <th>Value 3</th>
              </tr>
            </thead>
            <tbody>
              {Object.keys(responseData).map((key) => (
                <tr key={key}>
                  <td>{key}</td>
                  {responseData[key].map((value, index) => (
                    <td key={index}>{value}</td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}


      
    </div>
  );
}

   


export default App;
