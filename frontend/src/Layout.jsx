import { Route, Routes } from "react-router-dom";
import Home from "./pages/admin/Home"
import HomeUser from "./pages/user/Home"
import LoginForm from "./pages/auth/Login"
import { ToastContainer } from 'react-toastify'
import Card from "./pages/admin/card";
import PatientList from "./pages/admin/patientList";
import AddPatient from "./pages/admin/AddPatient";
import DoctorList from "./pages/admin/DoctorList";
import AddDoctor from "./pages/admin/AddDoctor";
import DoctorCard from "./pages/user/DoctorCard";
import Slider from "./pages/user/Slider";
import BookingPage from "./pages/user/BookingPage";
import EditDoctor from "./pages/admin/EditDoctor";

const  Layout = () => {
      return (
    <>
        <Routes>
            <Route path="login" element={<LoginForm />} />
            {/* <Route path="register" element={<Register />} /> */}
            <Route path="/" element={<HomeUser />} >
                <Route index element={<Slider />} />
                <Route path="doctors" element={<DoctorCard />} />  
                <Route path="doctors/book-appointment/:doctorNo" element={<BookingPage />} />  
            </Route>

            <Route path="admin" element={<Home />} >
                <Route index element={<Card />} />
                <Route path="dashboard" element={<Card />} />  
                <Route path="patient" element={<PatientList />} />  
                <Route path="add-patient" element={<AddPatient />} />  
                <Route path="doctor" element={<DoctorList />} />  
                <Route path="add-doctor" element={<AddDoctor />} />  
                <Route path="doctor/:id" element={<EditDoctor />} />  
                
                
            </Route>
            {/* <Route path="*" element={<NotFound />}></Route>  */}
        </Routes>
        <ToastContainer
                position="top-right"
                autoClose={5000}
                hideProgressBar={false}
                newestOnTop={false}
                closeOnClick={false}
                rtl={false}
                pauseOnFocusLoss
                draggable
                pauseOnHover
        />
    </>
  )
}
export default Layout;