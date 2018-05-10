const emptyData = {
  data: [],
}

export default {
  message: '',
  messages: [],
  user: {
    id: '',
    username: '',
    email: '',
    createdAt: '',
    isAdmin: false,
    isAuthenticated: false,
    firstName: '',
    lastName: '',
    bio: '',
    location: '',
    birthDate: '',
    picture: false
  },
  formData: {
    formData: {
      username: '',
      email: '',
      password: '',
      passwordConf: '',
    }
  },
  formProfile: {
    formProfile: {
      firstName: '',
      lastName: '',
      bio: '',
      location: '',
      birthDate: '',
      password: '',
      passwordConf: '',
    }
  },
  activities: {
    ...emptyData,
    pagination_end: false
  },
  // check if storing gpx content is OK
  gpx: null,
  sports: {
    ...emptyData,
  }
}
